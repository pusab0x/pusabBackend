import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User

from .models import ExamApplication, ExamCenter, ExamConfig


def payload(**overrides):
    data = {
        "name_bn": "রাকিব হাসান",
        "name_en": "md. rakib hasan",
        "mother_name": "মাতা",
        "father_name": "পিতা",
        "phone": "০১৭১২-৩৪৫৬৭৮",
        "photo_url": "https://res.cloudinary.com/demo/image/upload/a.jpg",
        "class_level": 8,
        "institution": "বিশ্বম্ভরপুর উচ্চ বিদ্যালয়",
        "village": "গ্রাম",
        "union": "ফতেপুর",
        "center": ExamCenter.objects.first().id,
        "payment_method": "bkash",
        "sender_number": "01812345678",
        "trx_id": "9kd7abc123",
    }
    data.update(overrides)
    return data


class ApplyAndStatusTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def apply(self, **overrides):
        return self.client.post("/api/exam/apply/", payload(**overrides), format="json")

    def test_status_returns_the_full_application(self):
        no = self.apply().data["application_no"]
        res = self.client.post("/api/exam/status/", {"application_no": no, "phone": "01712345678"}, format="json")
        self.assertEqual(res.status_code, 200)
        for field in ("mother_name", "father_name", "phone", "village", "union"):
            self.assertTrue(res.data[field])

    def test_bengali_fields_reject_english(self):
        for field in ("name_bn", "institution", "village"):
            res = self.apply(**{field: "Rakib Hasan"})
            self.assertEqual(res.status_code, 400)
            self.assertIn(field, res.data)

    def test_apply_assigns_number_and_normalizes(self):
        res = self.apply()
        self.assertEqual(res.status_code, 201, res.data)
        self.assertEqual(res.data["application_no"], "PUSAB-25-0001")
        app = ExamApplication.objects.get()
        self.assertEqual(app.phone, "01712345678")
        self.assertEqual(app.name_en, "MD. RAKIB HASAN")
        self.assertEqual(app.trx_id, "9KD7ABC123")
        self.assertEqual(app.amount, 50)
        self.assertEqual(self.apply(trx_id="OTHER12345").data["application_no"], "PUSAB-25-0002")

    def test_duplicate_trx_rejected(self):
        self.apply()
        res = self.apply(trx_id="9KD7ABC123")
        self.assertEqual(res.status_code, 400)
        self.assertIn("trx_id", res.data)

    def test_closed_when_deadline_passed(self):
        cfg = ExamConfig.load()
        cfg.deadline = datetime.date(2000, 1, 1)
        cfg.save()
        self.assertEqual(self.apply().status_code, 400)

    def test_status_needs_matching_phone(self):
        no = self.apply().data["application_no"]
        bad = self.client.post("/api/exam/status/", {"application_no": no, "phone": "01700000000"})
        self.assertEqual(bad.status_code, 404)
        ok = self.client.post("/api/exam/status/", {"application_no": no.lower(), "phone": "+8801712345678"})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.data["status"], "pending")
        self.assertFalse(ok.data["admit_available"])


class AdminFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        admin = User.objects.create_user(email="a@b.c", password="pw-12345-x", is_staff=True)
        self.client.force_authenticate(admin)
        public = APIClient()
        for i, cls in enumerate([9, 8, 8, 10]):
            res = public.post(
                "/api/exam/apply/",
                payload(class_level=cls, trx_id=f"TRX{i:05d}", phone=f"0171234567{i}"),
                format="json",
            )
            assert res.status_code == 201, res.data

    def test_verify_assign_rolls_and_admit(self):
        apps = list(ExamApplication.objects.order_by("id"))
        for app in apps[:3]:
            self.assertEqual(self.client.post(f"/api/exam/applications/{app.id}/verify/").status_code, 200)
        res = self.client.post(f"/api/exam/applications/{apps[3].id}/reject/", {"note": "TrxID মেলেনি"})
        self.assertEqual(res.data["status"], "rejected")

        self.assertEqual(self.client.post("/api/exam/applications/assign-rolls/").data["assigned"], 3)
        rolls = {a.id: (a.class_level, a.roll_no, a.serial_no) for a in ExamApplication.objects.all()}
        self.assertEqual(rolls[apps[1].id], (8, 8001, 1))
        self.assertEqual(rolls[apps[2].id], (8, 8002, 2))
        self.assertEqual(rolls[apps[0].id], (9, 9001, 3))
        self.assertIsNone(rolls[apps[3].id][1])

        # Running again assigns nothing new; a late verification continues the sequence.
        self.assertEqual(self.client.post("/api/exam/applications/assign-rolls/").data["assigned"], 0)
        self.client.post(f"/api/exam/applications/{apps[3].id}/reset/")
        self.client.post(f"/api/exam/applications/{apps[3].id}/verify/")
        res = self.client.post(f"/api/exam/applications/{apps[3].id}/assign-roll/")
        self.assertEqual((res.data["roll_no"], res.data["serial_no"]), (1001, 4))

        stats = self.client.get("/api/exam/applications/stats/").data
        self.assertEqual((stats["total"], stats["verified"], stats["collected"]), (4, 4, 200))

        # Admit card only once downloads are switched on.
        public = APIClient()
        body = {"application_no": apps[1].application_no, "phone": apps[1].phone, "mark_downloaded": True}
        self.assertFalse(public.post("/api/exam/status/", body).data["admit_available"])
        cfg = ExamConfig.load()
        cfg.admit_download_open = True
        cfg.save()
        self.assertTrue(public.post("/api/exam/status/", body).data["admit_available"])
        self.assertIsNotNone(ExamApplication.objects.get(pk=apps[1].id).admit_downloaded_at)

    def test_public_cannot_list(self):
        self.assertEqual(APIClient().get("/api/exam/applications/").status_code, 401)

    def test_offline_application_is_verified(self):
        data = payload(trx_id="", sender_number="")
        data.pop("payment_method")
        res = self.client.post("/api/exam/applications/", data, format="json")
        self.assertEqual(res.status_code, 201, res.data)
        self.assertEqual((res.data["status"], res.data["payment_method"]), ("verified", "offline"))

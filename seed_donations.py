from app.db.session import SessionLocal
from app.models.donation import DonationMethod, DonationMethodType

def seed_donation_methods():
    db = SessionLocal()
    try:
        # Bank Accounts
        methods = [
            DonationMethod(
                provider_name="Commercial Bank of Ethiopia",
                account_name="CSESE",
                account_number="1000XXXXXXXXXX",
                currency="ETB",
                method_type=DonationMethodType.BANK,
                display_order=1
            ),
            DonationMethod(
                provider_name="Awash Bank",
                account_name="CSESE",
                account_number="0143XXXXXXXXXX",
                currency="ETB",
                method_type=DonationMethodType.BANK,
                display_order=2
            ),
            DonationMethod(
                provider_name="Dashen Bank",
                account_name="CSESE",
                account_number="5860XXXXXXXXXX",
                currency="ETB",
                method_type=DonationMethodType.BANK,
                display_order=3
            ),
            # Mobile Wallets
            DonationMethod(
                provider_name="Telebirr",
                account_name="CSESE",
                account_number="09XXXXXXXX",
                currency="ETB",
                method_type=DonationMethodType.WALLET,
                display_order=4
            ),
            DonationMethod(
                provider_name="CBE Birr",
                account_name="CSESE",
                account_number="09XXXXXXXX",
                currency="ETB",
                method_type=DonationMethodType.WALLET,
                display_order=5
            )
        ]
        db.add_all(methods)
        db.commit()
        print("Donation methods seeded successfully.")
    except Exception as e:
        print(f"Error seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_donation_methods()

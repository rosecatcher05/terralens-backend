from app.database import SessionLocal
from app import models
from app.security import pwd_context


def create_admin():
    username = input("New username: ").strip()
    password = input("New password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    db = SessionLocal()

    try:
        existing = (
            db.query(models.Admin)
            .filter(models.Admin.username == username)
            .first()
        )

        if existing:
            print("Username already exists.")
            return

        hashed_password = pwd_context.hash(password)

        admin = models.Admin(
            username=username,
            password=hashed_password,
        )

        db.add(admin)
        db.commit()

        print(f"Admin '{username}' created successfully.")

    finally:
        db.close()


def delete_admin():
    username = input("Username to delete: ").strip()

    db = SessionLocal()

    try:
        admin = (
            db.query(models.Admin)
            .filter(models.Admin.username == username)
            .first()
        )

        if not admin:
            print("Admin not found.")
            return

        confirm = input(
            f"Delete '{username}'? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Cancelled.")
            return

        db.delete(admin)
        db.commit()

        print(f"Admin '{username}' deleted successfully.")

    finally:
        db.close()


def change_password():
    username = input("Username: ").strip()
    new_password = input("New password: ").strip()

    if not new_password:
        print("Password cannot be empty.")
        return

    db = SessionLocal()

    try:
        admin = (
            db.query(models.Admin)
            .filter(models.Admin.username == username)
            .first()
        )

        if not admin:
            print("Admin not found.")
            return

        admin.password = pwd_context.hash(new_password)

        db.commit()

        print(f"Password changed for '{username}'.")

    finally:
        db.close()


def list_admins():
    db = SessionLocal()

    try:
        admins = db.query(models.Admin).all()

        if not admins:
            print("No admin accounts found.")
            return

        print("\nAdmin accounts:")

        for admin in admins:
            print(f"- {admin.username}")

    finally:
        db.close()


def main():
    while True:
        print("\n==============================")
        print("   TerraLens Admin Manager")
        print("==============================")
        print("1. Create admin")
        print("2. Delete admin")
        print("3. Change password")
        print("4. List admins")
        print("5. Exit")
        print("==============================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_admin()

        elif choice == "2":
            delete_admin()

        elif choice == "3":
            change_password()

        elif choice == "4":
            list_admins()

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
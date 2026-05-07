from database import engine, Base
import models  # models.py deb saqlagan bo'lsangiz

# Barcha jadvallarni yaratadi
Base.metadata.create_all(bind=engine)

print("✅ Jadvallar yaratildi!")
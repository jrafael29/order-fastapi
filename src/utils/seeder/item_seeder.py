# src/seeders/item_seeder.py
from faker import Faker
import random

from fastapi import Depends
from sqlalchemy.orm import Session
from src.models import Item
from src.database import get_session

fake = Faker("pt_BR");


def seed_items(quantity: int = 10):
  session = next(get_session());
  print("inicio");
  if session.query(Item).count() > 0:
    print("Items já existem, pulando seed");
    return;

  items = [];
  for _ in range(quantity):
    item = Item(
      name=fake.word().capitalize(),
      description=fake.sentence(nb_words=10),
      sku=fake.unique.bothify(text="SKU-????-####").upper(),
      price=random.randint(1000, 50000),  # em centavos, ex: 1000 = R$10,00
      is_active=random.choice([True, True, True, False]),  # ~75% ativo
    );
    items.append(item);

  session.add_all(items);
  session.commit();
  print(f"{len(items)} items criados");



seed_items(10)
import os
import django
from django.core.files import File

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_project.settings')
django.setup()

from core.models import Category, Outfit

def seed_data():
    print("Seeding categories...")
    wedding, _ = Category.objects.get_or_create(name='Wedding Wear', slug='wedding-wear')
    party, _ = Category.objects.get_or_create(name='Party Wear', slug='party-wear')
    traditional, _ = Category.objects.get_or_create(name='Traditional', slug='traditional')
    designer, _ = Category.objects.get_or_create(name='Designer', slug='designer')

    print("Seeding outfits and images...")
    outfits_data = [
        {
            'name': 'Royal Red Bridal Lehenga',
            'category': wedding,
            'description': 'A stunning red lehenga with intricate gold embroidery, perfect for the modern bride looking for a traditional touch.',
            'price_per_day': 4500.00,
            'size': 'M',
            'stock': 2,
            'image_path': 'outfits/lehenga.png'
        },
        {
            'name': 'Midnight Blue Velvet Sherwani',
            'category': wedding,
            'description': 'Elegant midnight blue sherwani with silver work. Ideal for groomsmen or formal wedding receptions.',
            'price_per_day': 3500.00,
            'size': 'L',
            'stock': 3,
            'image_path': 'outfits/sherwani.png'
        },
        {
            'name': 'Emerald Green Silk Saree',
            'category': traditional,
            'description': 'Pure Banarasi silk saree with gold zari work. A classic choice for traditional ceremonies.',
            'price_per_day': 1800.00,
            'size': 'S',
            'stock': 5,
            'image_path': 'outfits/saree.png'
        },
        {
            'name': 'Sequinned Evening Gown',
            'category': party,
            'description': 'A dazzling rose gold gown covered in shimmering sequins. Perfect for gala nights and cocktail parties.',
            'price_per_day': 2500.00,
            'size': 'S',
            'stock': 1,
            'image_path': 'outfits/gown.png'
        },
        {
            'name': 'Tuxedo Black Suit',
            'category': party,
            'description': 'Sharp, tailored black tuxedo with satin lapels. Timeless elegance for any formal event.',
            'price_per_day': 2200.00,
            'size': 'XL',
            'stock': 4,
            'image_path': 'outfits/tuxedo.png'
        },
        {
            'name': 'Floral Printed Summer Dress',
            'category': designer,
            'description': 'Lightweight designer floral dress by Rose Atelier. Perfect for summer garden parties.',
            'price_per_day': 1200.00,
            'size': 'M',
            'stock': 3,
            'image_path': 'outfits/summer_dress.png'
        }
    ]

    for item in outfits_data:
        outfit, created = Outfit.objects.update_or_create(
            name=item['name'],
            defaults={
                'category': item['category'],
                'description': item['description'],
                'price_per_day': item['price_per_day'],
                'size': item['size'],
                'stock': item['stock'],
                'image': item['image_path']
            }
        )
        print(f"Updated/Created outfit: {outfit.name}")

    print("Seeding complete!")

if __name__ == '__main__':
    seed_data()

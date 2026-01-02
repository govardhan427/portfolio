import json
from django.apps import apps
from django.db import transaction

print("🚀 Starting data load...")

# Load the data
with open('initial_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📄 Found {len(data)} items to load.")

success_count = 0
error_count = 0

for item in data:
    try:
        model_str = item['model']
        app_label, model_name = model_str.split('.')
        Model = apps.get_model(app_label, model_name)
        
        fields = item['fields']
        pk = item['pk']
        
        # Save securely
        with transaction.atomic():
            obj, created = Model.objects.update_or_create(pk=pk, defaults=fields)
            
        success_count += 1
        if success_count % 50 == 0:
            print(f"✅ Loaded {success_count} items...")
            
    except Exception as e:
        print(f"❌ ERROR on {item.get('model')} ID {item.get('pk')}: {e}")
        error_count += 1

print(f"\n🎉 DONE! Success: {success_count}, Errors: {error_count}")
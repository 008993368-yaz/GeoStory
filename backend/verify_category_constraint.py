"""Quick verification that enum-generated SQL matches the original constraint."""

from app.constants import StoryCategory

# Original constraint from Alembic migration
original_constraint = "category IN ('travel', 'food', 'history', 'culture', 'nature', 'urban', 'personal')"

# Generated constraint from enum
generated_constraint = StoryCategory.sql_check_constraint()

print("=" * 70)
print("Category Validation Constraint Verification")
print("=" * 70)
print()
print("Original constraint (from Alembic migration):")
print(f"  {original_constraint}")
print()
print("Generated constraint (from StoryCategory enum):")
print(f"  {generated_constraint}")
print()
print("Match:", "✅ YES" if original_constraint == generated_constraint else "❌ NO")
print()

# Verify all enum values
print("All category values:")
for category in StoryCategory:
    print(f"  - {category.value}")
print()
print("Total categories:", len(StoryCategory.values()))
print()
print("=" * 70)
print("✅ Verification complete!")
print("=" * 70)

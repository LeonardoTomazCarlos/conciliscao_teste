from app import app

print("🔍 Listando todas as rotas registradas no Flask:")
print("-" * 50)

for rule in app.url_map.iter_rules():
    methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"{rule.rule:<40} [{methods}]")

print("-" * 50)
print(f"Total de rotas: {len(list(app.url_map.iter_rules()))}")

# Verificar especificamente a rota que está dando problema
conciliacao_route = None
for rule in app.url_map.iter_rules():
    if '/api/conciliacao/executar' in rule.rule:
        conciliacao_route = rule
        break

if conciliacao_route:
    print(f"✅ Rota encontrada: {conciliacao_route.rule} [{', '.join(sorted(conciliacao_route.methods - {'HEAD', 'OPTIONS'}))}]")
else:
    print("❌ Rota /api/conciliacao/executar NÃO encontrada!")

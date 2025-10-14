from nlp_parser import NLPParser

parser = NLPParser()

queries = [
    'Can I invest in Apple today?',
    'Should I buy Tesla stock?',
    'Is Reliance a good investment?',
    'AAPL',
    'How many shares of Microsoft should I buy?'
]

print("NLP Parser Test")
print("=" * 60)

for q in queries:
    result = parser.parse_query(q)
    print(f"\nQuery: '{q}'")
    print(f"  Symbol: {result['symbol']}")
    print(f"  Company: {result.get('company_name')}")
    print(f"  Intent: {result['intent']}")
    print(f"  Quantity: {result.get('quantity')}")
    print(f"  Confidence: {result['confidence']:.2f}")

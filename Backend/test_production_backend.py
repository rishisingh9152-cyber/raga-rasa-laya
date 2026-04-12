"""
Test production backend
"""
import requests
import json

base_url = 'https://raga-rasa-backend.onrender.com'

print('\n' + '='*70)
print('TESTING PRODUCTION BACKEND')
print('='*70 + '\n')

print('Testing /recommendations endpoint...')
print('-' * 70)

try:
    url = f'{base_url}/recommendations?emotion=happy'
    resp = requests.get(url, timeout=15)
    
    print(f'Status Code: {resp.status_code}')
    
    content_type = resp.headers.get('content-type', 'NOT SET')
    print(f'Content-Type: {content_type}')
    
    print(f'Response Length: {len(resp.text)} chars')
    print(f'First 500 chars:')
    print(resp.text[:500])
    
    print('\nAttempting to parse as JSON...')
    try:
        data = resp.json()
        print(f'✓ Valid JSON!')
        print(f'Keys: {list(data.keys())}')
        
        if 'recommendations' in data:
            recs = data['recommendations']
            print(f'\nRecommendations count: {len(recs)}')
            if recs:
                first = recs[0]
                print(f'\nFirst song:')
                for key, val in first.items():
                    print(f'  {key}: {str(val)[:100]}')
    except json.JSONDecodeError as e:
        print(f'✗ INVALID JSON')
        print(f'Error: {e}')
        print(f'\nThis means the backend is returning HTML (error page) instead of JSON')
        
except Exception as e:
    print(f'Connection Error: {e}')

print('\n' + '='*70 + '\n')

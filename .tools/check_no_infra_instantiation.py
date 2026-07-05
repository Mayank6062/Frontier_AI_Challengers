import os, re, sys
ROOT='src/backend/api'
patterns=['CacheService\s*\(','StorageService\s*\(','SessionStore\s*\(','EngagementStore\s*\(','SecretsManager\s*\(','LedgerService\s*\(','LLMClient\s*\(','Logger\s*\(','Metrics\s*\(']
violations=[]
for root,_,files in os.walk(ROOT):
    for f in files:
        if f.endswith('.py'):
            p=os.path.join(root,f)
            s=open(p,encoding='utf8').read()
            for pat in patterns:
                if re.search(pat,s):
                    violations.append((p,pat))
print('FOUND',len(violations),'instantiations')
for v in violations:
    print(v[0])
if violations:
    sys.exit(2)
print('NO_DIRECT_INSTANTIATIONS')

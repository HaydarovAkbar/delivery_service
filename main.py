from openai import OpenAI

OPENAI_KEY = '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'
ORGANIZATION_ID = 'org-nikZJpRdZSBtqUGYfMXbvqRL'

client = OpenAI(
    organization=ORGANIZATION_ID,
    api_key=OPENAI_KEY,
)
models = client.models.list()

print(models)

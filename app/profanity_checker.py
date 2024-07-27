from googleapiclient import discovery
from app.config import settings


def detect_toxicity(text: str) -> bool:
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=settings.api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return score > 0.7

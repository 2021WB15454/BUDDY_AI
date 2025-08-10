"""
Test script for datetime functionality
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(__file__))

from core.nlp_processor import NLPProcessor
from utils.config import Config

async def test_datetime_intent():
    config = Config()
    nlp = NLPProcessor(config)
    
    test_queries = [
        'date',
        'what is today',
        'current time',
        'what day is today',
        'tomorrow'
    ]
    
    print('🧪 Testing DateTime Intent Detection')
    print('=' * 50)
    
    for query in test_queries:
        result = await nlp.process(query)
        intent = result.get('intent', 'unknown')
        print(f'Query: \'{query}\' -> Intent: {intent}')
        print('-' * 30)

if __name__ == "__main__":
    asyncio.run(test_datetime_intent())

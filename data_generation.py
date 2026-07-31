import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import random

def generate_event_log(num_users=20000):
    events = []
    
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_users):
        borrower_id = str(uuid.uuid4())
        
        # User signup timestamp
        current_time = start_date + timedelta(days=random.randint(0, 365), minutes=random.randint(0, 1440))
        
        # 1. Signup
        events.append({
            'event_id': str(uuid.uuid4()),
            'borrower_id': borrower_id,
            'event_type': 'signup',
            'event_timestamp': current_time
        })
        
        # 2. Browse
        if random.random() > 0.10: # 90% proceed
            current_time += timedelta(minutes=random.randint(5, 120))
            events.append({
                'event_id': str(uuid.uuid4()),
                'borrower_id': borrower_id,
                'event_type': 'browse',
                'event_timestamp': current_time
            })
            
            # 3. Apply
            if random.random() > 0.60: # 40% proceed
                current_time += timedelta(minutes=random.randint(10, 60))
                events.append({
                    'event_id': str(uuid.uuid4()),
                    'borrower_id': borrower_id,
                    'event_type': 'apply',
                    'event_timestamp': current_time
                })
                
                # 4. Funded
                if random.random() > 0.20: # 80% proceed
                    current_time += timedelta(days=random.randint(1, 7))
                    events.append({
                        'event_id': str(uuid.uuid4()),
                        'borrower_id': borrower_id,
                        'event_type': 'funded',
                        'event_timestamp': current_time
                    })
                    
                    # 5. Repaid
                    if random.random() > 0.15: # 85% proceed
                        current_time += timedelta(days=random.randint(30, 90))
                        events.append({
                            'event_id': str(uuid.uuid4()),
                            'borrower_id': borrower_id,
                            'event_type': 'repaid',
                            'event_timestamp': current_time
                        })
                        
                        # 6. Repeat Apply
                        if random.random() > 0.70: # 30% proceed
                            current_time += timedelta(days=random.randint(10, 180))
                            events.append({
                                'event_id': str(uuid.uuid4()),
                                'borrower_id': borrower_id,
                                'event_type': 'repeat_apply',
                                'event_timestamp': current_time
                            })

    df = pd.DataFrame(events)
    df = df.sort_values(by='event_timestamp').reset_index(drop=True)
    df.to_csv('synthetic_event_log.csv', index=False)
    print(f"Generated {len(df)} events for {num_users} users.")

if __name__ == "__main__":
    generate_event_log()

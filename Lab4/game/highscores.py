import json
import os

MAX_ENTRIES=5
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # folder that holds main.py
HIGHSCORE_FILE=os.path.join(ROOT,"highscores.json")

def load_scores(path=None):
    """Top scores, best first. Missing / unreadable / corrupt file -> empty list."""
    path=path or HIGHSCORE_FILE
    try:
        with open(path,"r",encoding="utf-8") as f:
            data=json.load(f)
    except (OSError,ValueError,RecursionError):   # missing, unreadable, not valid JSON
        return []
    if not isinstance(data,list):
        return []
    scores=[s for s in data if isinstance(s,int) and not isinstance(s,bool) and s>0]
    return sorted(scores,reverse=True)[:MAX_ENTRIES]

def save_scores(scores,path=None):
    """Write atomically. Returns False (never raises) if the file can't be written."""
    path=path or HIGHSCORE_FILE
    tmp=path+".tmp"
    try:
        with open(tmp,"w",encoding="utf-8") as f:
            json.dump(scores,f)
        os.replace(tmp,path)
        return True
    except OSError:
        try: os.remove(tmp)
        except OSError: pass
        return False

def add_score(score,path=None):
    """Insert a score. Returns (top_scores, rank) where rank is the 0-based
    position of the new score, or None if it didn't make the top 5."""
    scores=load_scores(path)
    rank=sum(1 for s in scores if s>=score)   # ties go below existing equal scores
    if score<=0 or rank>=MAX_ENTRIES:
        return scores,None
    scores.insert(rank,score)
    scores=scores[:MAX_ENTRIES]
    save_scores(scores,path)
    return scores,rank

import pandas as pd


DEFAULT_SUBREDDITS = set([
    "/r/AskReddit",
    "/r/announcements",
    "/r/funny",
    "/r/pics",
    "/r/todayilearned",
    "/r/science",
    "/r/IAmA",
    "/r/blog",
    "/r/videos",
    "/r/worldnews",
    "/r/gaming",
    "/r/movies",
    "/r/Music",
    "/r/aww",
    "/r/news",
    "/r/gifs",
    "/r/askscience",
    "/r/explainlikeimfive",
    "/r/EarthPorn",
    "/r/books",
    "/r/television",
    "/r/LifeProTips",
    "/r/sports",
    "/r/DIY",
    "/r/Showerthoughts",
    "/r/space",
    "/r/Jokes",
    "/r/tifu",
    "/r/food",
    "/r/photoshopbattles",
    "/r/Art",
    "/r/InternetIsBeautiful",
    "/r/mildlyinteresting",
    "/r/GetMotivated",
    "/r/history",
    "/r/nottheonion",
    "/r/gadgets",
    "/r/dataisbeautiful",
    "/r/Futurology",
    "/r/Documentaries",
    "/r/listentothis",
    "/r/personalfinance",
    "/r/philosophy",
    "/r/nosleep",
    "/r/creepy",
    "/r/OldSchoolCool",
    "/r/UpliftingNews",
    "/r/WritingPrompts",
    "/r/TwoXChromosomes",
])

def get_popular_subreddits() -> pd.DataFrame:
    # This was generated from https://frontpagemetrics.com/top-sfw-subreddits/offset/
    # as of 2022-04-03
    return pd.read_csv("popular_subreddits.csv", delimiter=r"\s+")



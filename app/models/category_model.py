from enum import Enum


class Category(str, Enum):
    """This is not a full of categories of law, just a small section as an example."""

    asylum = "Applying for asylum or permission to stay in the UK"
    crime = "Crime/Criminal Law"
    debt = "Debt, money problems and bankruptcy"
    family = "Family, marriage, separation and children"
    housing = "Housing, eviction and homelessness"
    welfare = "Welfare benefits appeals,"

# NFL Draft Model 2.0

## Dataset

Data is scraped from NFL Draft Scout, Pro Football Reference, and CFB Reference.

The dataset covers the 2006-2014 draft classes and includes players who were ranked in NFL Draft Scout's top 300 in their draft year.  I have removed all quarterbacks, kickers, punters, long snappers, and fullbacks due to the relatively small sample sizes or extreme specialization that each position requires. For now the model focuses exclusively on 13 "skill" positions, bucketed into 7 position groups.

The dataset restrictions exclude some notable players ranked outside of the top 300, both drafted and undrafted, who went on to varying degrees of success in the NFL.  At the top extreme are 4-time All Pro Antonio Brown and Super Bowl LIII MVP Julian Edelman.  But while many players on this list never played a down in the NFL, it is important to be aware of which players are excluded.

I have removed players from the dataset whose NFL careers were cut prematurely short either voluntarily or involuntarily (due to injury, not ability).  These players' ratings are not representative of their production and thus only serve to complicate the dataset and confuse any modeling attempts. Examples include Aaron Hernandez, Gaines Adams, and Chris Borland.  

There is also a subset of players who drastically changed position upon entering the league.  This is contrary to less extreme position changes.  These players have been removed because their college statistics create noisy data.  Examples: Denard Robinson, Devin Hester, J.R. Sweezy.

## Goal

Build an NFL draft model capable of producing meaningful player predictions.

A Random Forest model is appropriate for this dataset because of the small number of observations (250-300 players per class) and the non-linear relationship between input and output variables. Random Forests are fairly robust against overfitting.

Player performance is impacted by round and team selection in the draft. First round picks receive more opportunities than later round selections, different schemes fit players better. Because of this the model performance can be improved by including some regression to the draft selection.

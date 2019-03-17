## 1. Overview
A comprehensive judging platform for hackathons

## 2. Installation
- Created with Django in a Docker container
- Hopefully will be deployable on Heroku soon

To dev locally:
- Clone repo. `git clone <>`
- Spin up. `docker-compose up`
- Open at `localhost:8052` with un:admin & pw:HackathonsRule!
    - Otherwise, create superuser `python manage.py createsuperuser`

## 3. Motivation
- Judging is a hard problem
    - One of the main problems is judge scores are unreliable
    - One solution was relative scoring with Gavel
    - However, given restraints, this was not possible at HooHacks
- Our solution was normalized averages
- Normalization reduces variability between judges (not for each judge)
    - Assumption 1. Some judges simply grade things more harshly than other judges
    - Assumption 2. The distribution of scores for each team is normally distributed
    - Assumption 3. The variance for each team's score distribution is the same
    - Observation. The moving average of judge scores steadily increases throughout the judging time.
- We collect this information by running a normalization session where every judge evaluates a couple "fake" projects before real judging begins
- The empirical evidence is alright
    - For each criteria (e.g. functionality, impact, creativity), if judge A's score was >= judge B's score in the normalization session, then the same held true for any project roughly 65-85% of the time.
        - Note, the fact that judges did not agree on what was more creative or more impactful (though impactful was the most agreeable of our criteria) indicates the criteria we used were subjective. And that's acceptable. Reducing what makes a project "good" into a reasonable number of _objective_ criteria is an exercise in futility.
    - The distribution of scores for the normalization "anchor" demos was (surprisingly) normally distributed so assumption 2 seems to hold.
- In conclusion, this method isn't perfect, but it's a reasonable step up from just averages
    - Further, there are some interesting judging ideas that run orthogonal to score normalization. For example, imagine if every team's score was actually represented as a confidence interval. Every time a judge evaluates a team, the team's confidence interval shrinks toward its "true" score. Once a team is confidently out of the race, judges can stop evaluating them and start judging teams closer to the top. At the end of the day, the accuracy of the top rankings is important than that of the bottom rankings. This is effectively a linear bandit problem so we can probably apply some state-of-the-art reinforcement learning solutions?

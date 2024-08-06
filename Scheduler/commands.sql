CREATE TASK minus_task SERVER = 1 SCHEDULE = '1 MINUTE' AS minus(7, b=3, c=2)
CREATE TASK times_task SERVER = 1 SCHEDULE = '1 MINUTE' AS times_task(a=1, b=2)
CREATE TASK plusminus_task SERVER = 3 AFTER times_task AS plusminus_task(a=4, b=6, c=7)
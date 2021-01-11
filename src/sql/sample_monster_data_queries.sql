-- All monsters with type, sub-type (region), and description.
SELECT m.Monster, d.Derivation, r.Region, m.Description
  FROM Monster m
  JOIN Derivation d ON m.DerivationID = d.Id
  JOIN Region r     ON m.RegionID = r.Id;
  
-- Number of each attack type per monster. 
SELECT d.Derivation, COUNT(CASE WHEN a.StatUsed LIKE "Pow%" THEN 1 END) 'Power Attacks', COUNT(CASE WHEN a.StatUsed LIKE "Int%" THEN 1 END) 'Int Attacks'
  FROM Attack a
  JOIN Derivation d on a.DerivationId = d.Id
  GROUP BY DerivationId


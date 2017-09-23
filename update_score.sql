DELIMITER //
CREATE PROCEDURE update_score(IN game_id int, IN user_id int, IN score double)
   BEGIN
      INSERT INTO Scores (GameID, PlayerID, Score) VALUES (game_id, user_id, score)
         ON DUPLICATE KEY UPDATE Score = score; 
      SELECT p.Name as User, g.Name as Game, s.Score 
         FROM Scores as s 
         JOIN Players as p ON p.ID = s.PlayerID 
         JOIN Games as g ON g.ID = s.GameID 
         WHERE g.ID = game_id AND p.ID = user_id;
   END//
DELIMITER ;
DELIMITER //
CREATE PROCEDURE get_or_create_user(IN name VARCHAR(255), IN slack_team_id VARCHAR(255), IN slack_id VARCHAR(255))
   BEGIN
   	  DECLARE team_id INT;
   	  SET team_id = (SELECT ID FROM Teams WHERE SlackTeamID = slack_team_id);

      IF EXISTS (SELECT * FROM Players WHERE SlackID = slack_id AND TeamID = team_id) THEN 
         SELECT ID FROM Players WHERE SlackID = slack_id AND TeamID = team_id;
      ELSE 
         INSERT INTO Players (TeamID, Name, SlackID) VALUES (team_id, name, slack_id); 
         SELECT LAST_INSERT_ID() as "ID"; 
      END IF;
   END//
DELIMITER ;
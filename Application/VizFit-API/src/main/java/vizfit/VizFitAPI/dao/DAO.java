package vizfit.VizFitAPI.dao;

import java.security.NoSuchAlgorithmException;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.PreparedStatementSetter;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import vizfit.VizFitAPI.Models.User;
import vizfit.VizFitAPI.Models.Session;
import vizfit.VizFitAPI.Models.Workout;
import vizfit.VizFitAPI.utilities.Utilities;

@Repository("DAOInterface")
public class DAO implements DAOInterface{
	
	@Autowired
	private JdbcTemplate jdbcTemplate;
	
	@Override
	public Collection<User> findAll(){
		return jdbcTemplate.query("SELECT * FROM USERS;", new BeanPropertyRowMapper<User>(User.class));
	}
	@Override
	@Transactional
	public User login(String username, String password) throws NoSuchAlgorithmException {
		
		String passwordHash = Utilities.digest(password);
		
		List<User> user = jdbcTemplate.query("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?;", 
			    new PreparedStatementSetter() {
					public void setValues(PreparedStatement preparedStatement) throws SQLException {
							preparedStatement.setString(1, username);
							preparedStatement.setString(2, passwordHash);
					}
				}, new BeanPropertyRowMapper<User>(User.class));
		
		
		
		if(user.size() > 0) {
			
			User newUser = user.get(0);
			
			Date d = new Date();
			
			String token = Utilities.digest(newUser.getUserId() + newUser.getUserId() + d.toString());
			
			List<Session> sessions = jdbcTemplate.query("SELECT * FROM SESSIONS WHERE USER_ID = ?;", 
				    new PreparedStatementSetter() {
						public void setValues(PreparedStatement preparedStatement) throws SQLException {
								preparedStatement.setInt(1, newUser.getUserId());
						}
					}, new BeanPropertyRowMapper<Session>(Session.class));
			
			int rowsAffected = 0;
			
			if(sessions.size() == 1) {
				rowsAffected = jdbcTemplate.update("UPDATE SESSIONS SET TOKEN = ? WHERE USER_ID = ?;", 
					    new PreparedStatementSetter() {
							public void setValues(PreparedStatement preparedStatement) throws SQLException {
									preparedStatement.setString(1, token);
									preparedStatement.setInt(2, newUser.getUserId());
							}
						});
			} else {
				rowsAffected = jdbcTemplate.update("INSERT INTO SESSIONS (SESSION_ID, USER_ID, TOKEN) VALUES (0,?,?);", 
					    new PreparedStatementSetter() {
							public void setValues(PreparedStatement preparedStatement) throws SQLException {
									preparedStatement.setInt(1, newUser.getUserId());
									preparedStatement.setString(2, token);
							}
						});
			}
			
			
					
			if(rowsAffected == 1) {
				
				newUser.setToken(token); 
				
				return newUser;
			} else {
				throw new RuntimeException("More than 1 row affected.");
			}
			
		}
		
		return new User();
	}
	@Transactional
	public User loginWithCookie(String username, String userId, String token) throws NoSuchAlgorithmException {
		
		
		List<User> user = jdbcTemplate.query("SELECT *"
				+ " FROM "
				+ " (SELECT USER_ID, USERNAME FROM USERS WHERE USER_ID = ? AND USERNAME = ?) U "
				+ " INNER JOIN "
				+ " (SELECT USER_ID FROM SESSIONS WHERE USER_ID = ? AND TOKEN = ?) S "
				+ " ON U.USER_ID = S.USER_ID;", 
			    new PreparedStatementSetter() {
					public void setValues(PreparedStatement preparedStatement) throws SQLException {
							preparedStatement.setString(1, userId);
							preparedStatement.setString(2, username);
							preparedStatement.setString(3, userId);
							preparedStatement.setString(4, token);
					}
				}, new BeanPropertyRowMapper<User>(User.class));
		
		
		
		if(user.size() > 0) {
			
			User newUser = user.get(0);
			
			Date d = new Date();
			
			String newToken = Utilities.digest(newUser.getUserId() + newUser.getUserId() + d.toString()); 
			newUser.setToken(newToken);
			int rowsAffected = jdbcTemplate.update("UPDATE SESSIONS SET TOKEN = ? WHERE USER_ID = ?;", 
				    new PreparedStatementSetter() {
						public void setValues(PreparedStatement preparedStatement) throws SQLException {
								preparedStatement.setString(1, newToken);
								preparedStatement.setInt(2, newUser.getUserId());
						}
					});
			if(rowsAffected > 1) {
				throw new RuntimeException("More than 1 row affected.");
			}
			return newUser;
		}
		
		return new User();
	}
	@Override
	@Transactional
	public Collection<User> getLeaderboard() throws NoSuchAlgorithmException {
		
		Collection<User> leaderboard = jdbcTemplate.query("SELECT USERNAME, ROW_NUMBER() OVER(ORDER BY TOTAL DESC) AS RANKED, PUSHUPS, SITUPS, SQUATS, TOTAL "
								   +" FROM USERS AS U "
								      +" JOIN "
								      +" (SELECT USER_ID, SUM(PUSHUPS) PUSHUPS, SUM(SITUPS) SITUPS, SUM(SQUATS) SQUATS," 								       	+" (SUM(PUSHUPS) + SUM(SQUATS) + SUM(SITUPS)) TOTAL "
									+" FROM WORKOUTS "
									+" GROUP BY USER_ID) AS W "
								      +" ON W.USER_ID = U.USER_ID;", 
				new BeanPropertyRowMapper<User>(User.class));
		
		return leaderboard;
	}
	@Override
	@Transactional
	public int register(String username, String password) throws NoSuchAlgorithmException {
		
		String passwordHash = Utilities.digest(password);
		
		List<User> user = jdbcTemplate.query("SELECT * FROM USERS WHERE USERNAME = ?;", 
			    new PreparedStatementSetter() {
					public void setValues(PreparedStatement preparedStatement) throws SQLException {
							preparedStatement.setString(1, username);
					}
				}, new BeanPropertyRowMapper<User>(User.class));
		
		if(user.size() == 0) {
			
			int rowsAffected = jdbcTemplate.update("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?,?);", 
				    new PreparedStatementSetter() {
						public void setValues(PreparedStatement preparedStatement) throws SQLException {
								preparedStatement.setString(1, username);
								preparedStatement.setString(2, passwordHash);
						}
					});
			
			
			if(rowsAffected > 1) {
				throw new RuntimeException("More than 1 row affected.");
			}
			
			return rowsAffected;
		} else {
			return -999;
		}
	}
	@Override
	public Collection<Workout> getAllWorkoutsForUserId(int userId) {
		
		Collection<Workout> workoutList = jdbcTemplate.query("SELECT * FROM WORKOUTS WHERE USER_ID = ?;", 
				new PreparedStatementSetter() {
					public void setValues(PreparedStatement preparedStatement) throws SQLException {
							preparedStatement.setInt(1, userId);
					}
				}, new BeanPropertyRowMapper<Workout>(Workout.class));
		
		return workoutList;
	}
	@Override
	@Transactional
	public int createWorkout(Workout workout) {
		
		int rowsAffected = jdbcTemplate.update("INSERT INTO WORKOUTS(USER_ID, WORKOUT_START_TIME, WORKOUT_END_TIME, PUSHUPS, SITUPS, SQUATS) VALUES(?,?,?,?,?,?);", 
				new PreparedStatementSetter() {
					public void setValues(PreparedStatement preparedStatement) throws SQLException {
							preparedStatement.setInt(1, workout.getUserId());
							preparedStatement.setTimestamp(2, workout.getWorkoutStartTime());
							preparedStatement.setTimestamp(3, workout.getWorkoutEndTime());
							preparedStatement.setInt(4, workout.getPushups());
							preparedStatement.setInt(5, workout.getSitups());
							preparedStatement.setInt(6, workout.getSquats());
							
					}
				});
		if(rowsAffected > 1) {
			throw new RuntimeException("More than 1 row affected.");
		}
		return rowsAffected;
	}
}

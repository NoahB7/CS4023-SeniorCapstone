package vizfit.VizFitAPI.dao;

import java.security.NoSuchAlgorithmException;
import java.util.Collection;
import vizfit.VizFitAPI.Models.User;
import vizfit.VizFitAPI.Models.Workout;

public interface DAOInterface {

	public Collection<User> findAll();
	
	public User login(String username, String password) throws NoSuchAlgorithmException;

	public int register(String username, String password) throws NoSuchAlgorithmException;

	public Collection<Workout> getAllWorkoutsForUserId(int userId);

	public int createWorkout(Workout workout);

	public Collection<User> getLeaderboard() throws NoSuchAlgorithmException;

	public User loginWithCookie(String username, String userId, String token) throws NoSuchAlgorithmException;

}

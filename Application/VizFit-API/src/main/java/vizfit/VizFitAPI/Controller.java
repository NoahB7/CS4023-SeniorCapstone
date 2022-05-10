package vizfit.VizFitAPI;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import vizfit.VizFitAPI.Models.User;
import vizfit.VizFitAPI.Models.Workout;
import vizfit.VizFitAPI.dao.DAOInterface;
import vizfit.VizFitAPI.utilities.Utilities;

@RestController
public class Controller {
	
	private DAOInterface dao;
	public DAOInterface getDAO() {
		return dao;
	}

	@Autowired
    public void setJdbcDAO(DAOInterface dao) {
		this.dao = dao;
	}

	@RequestMapping("/test")
	public String test() {
		String x = Utilities.digest("x");
		return x;
	}
	@RequestMapping("/test2")
	public List<String> test2() {
		
		
		ArrayList<String> x = new ArrayList<>();
		
		for(int i = 0; i < 20; i++) {
			x.add(i, "ldfasf" + i);
		}
		return x;
		
		
	}
	@RequestMapping("/getUser")
	public Collection<User> listUser() throws IOException, NoSuchAlgorithmException {

		DAOInterface dao = getDAO();

		Collection<User> listUser = dao.findAll();
		
		return listUser;
	}
	@RequestMapping("/getLeaderboard")
	public Collection<User> getLeaderboard() throws IOException, NoSuchAlgorithmException {

		DAOInterface dao = getDAO();

		Collection<User> leaderboard = dao.getLeaderboard();
		
		return leaderboard;
	}
	@PostMapping("/login")
	public User login(@RequestBody Map<String, String> payload) throws IOException, NoSuchAlgorithmException {

		DAOInterface dao = getDAO();

		User user = dao.login(payload.get("username"), payload.get("password"));

		return user;
	}
	@PostMapping("/loginWithCookie")
	public User loginWithCookie(@RequestBody Map<String, String> payload) throws IOException, NoSuchAlgorithmException {

		DAOInterface dao = getDAO();

		User user = dao.loginWithCookie(payload.get("username"), payload.get("userId"), payload.get("token"));

		return user;
	}
	@PostMapping("/register")
	public int listUser(@RequestBody Map<String, String> payload) throws IOException, NoSuchAlgorithmException {

		DAOInterface dao = getDAO();
		
		int rowsAffected = dao.register(payload.get("username"), payload.get("password"));

		return rowsAffected;
	}
	@PostMapping("/getAllWorkoutsForUserId")
	public Collection<Workout> getAllWorkoutsForUserId(@RequestBody Map<String, Integer> payload) throws IOException {

		DAOInterface dao = getDAO();
		
		Collection<Workout> workoutList = dao.getAllWorkoutsForUserId(payload.get("userId"));

		return workoutList;
	}
	@PostMapping("/createWorkout")
	public int createWorkout(@RequestBody Map<String, Workout> payload) throws IOException {

		DAOInterface dao = getDAO();
		
		int rowsAffected = dao.createWorkout(payload.get("workout"));

		return rowsAffected;
	}
	
//	@RequestMapping("/testDB")
//	public DataSource testDB() {
//		
//		//String sql = "SELECT * FROM USER LEFT JOIN WORKOUT ON WORKOUT.USER_ID = USER.USER_ID WHERE WORKOUT.USER_ID = USER.USER_ID;";
//        
//        DataSource result = jdbcTemplate.getDataSource();
//         
//        System.out.println(result);
//        return result;
//	}
}

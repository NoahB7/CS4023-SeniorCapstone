package vizfit.VizFitAPI.Models;


public class User{

	
	private int userId;
	private int ranked;
	private int pushups;
	private int situps;
	private int squats;
	private int total;
	private String username;
	private String password;
	private String token;
	
	public int getUserId() {
		return userId;
	}
	public void setUserId(int user_id) {
		this.userId = user_id;
	}
	public int getRanked() {
		return ranked;
	}
	public void setRanked(int ranked) {
		this.ranked = ranked;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	public int getSquats() {
		return squats;
	}
	public void setSquats(int squats) {
		this.squats = squats;
	}
	public int getTotal() {
		return total;
	}
	public void setTotal(int total) {
		this.total = total;
	}
	public int getPushups() {
		return pushups;
	}
	public void setPushups(int pushups) {
		this.pushups = pushups;
	}
	public int getSitups() {
		return situps;
	}
	public void setSitups(int situps) {
		this.situps = situps;
	}
	public String getToken() {
		return token;
	}
	public void setToken(String token) {
		this.token = token;
	}

}

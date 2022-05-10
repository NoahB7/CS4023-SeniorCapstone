package vizfit.VizFitAPI.Models;

import java.sql.Timestamp;

public class Workout {

	private int workoutId;
	private int userId;
	private Timestamp workoutStartTime;
	private Timestamp workoutEndTime;
	private int pushups;
	private int situps;
	private int squats;
	
	public int getWorkoutId() {
		return workoutId;
	}
	public void setWorkoutId(int workoutId) {
		this.workoutId = workoutId;
	}
	public int getUserId() {
		return userId;
	}
	public void setUserId(int userId) {
		this.userId = userId;
	}
	public Timestamp getWorkoutStartTime() {
		return workoutStartTime;
	}
	public void setWorkoutStartTime(Timestamp workoutStartTime) {
		this.workoutStartTime = workoutStartTime;
	}
	public Timestamp getWorkoutEndTime() {
		return workoutEndTime;
	}
	public void setWorkoutEndTime(Timestamp workoutEndTime) {
		this.workoutEndTime = workoutEndTime;
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
	public int getSquats() {
		return squats;
	}
	public void setSquats(int squats) {
		this.squats = squats;
	}
}

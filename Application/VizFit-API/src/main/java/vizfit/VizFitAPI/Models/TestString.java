package vizfit.VizFitAPI.Models;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class TestString {
	@Id
	private String testString;

	public String getTestString() {
		return testString;
	}

	public void setTestString(String testString) {
		this.testString = testString;
	}
}

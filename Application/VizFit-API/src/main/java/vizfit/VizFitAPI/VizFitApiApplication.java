package vizfit.VizFitAPI;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import vizfit.VizFitAPI.dao.DAO;


@SpringBootApplication
public class VizFitApiApplication {
	
	@Autowired
	DAO dao;
	
	public static void main(String[] args) {
		SpringApplication.run(VizFitApiApplication.class, args);
	}
}

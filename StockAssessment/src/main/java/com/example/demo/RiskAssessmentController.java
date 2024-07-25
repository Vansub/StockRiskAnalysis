package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@CrossOrigin(origins = "http://localhost:3000")
public class RiskAssessmentController {

    @Autowired
    private RestTemplate restTemplate;

    @PostMapping("/predict_and_recommend")
    public ResponseEntity<?> predictAndRecommend(@RequestBody Map<String, Object> payload) {
    	String flaskUrl = "http://localhost:8080/predict_and_recommend"; // Flask running on port 8080
        ResponseEntity<Map> response = restTemplate.postForEntity(flaskUrl, payload, Map.class);
        return ResponseEntity.ok(response.getBody());
    }
}

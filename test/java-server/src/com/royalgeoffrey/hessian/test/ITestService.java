package com.royalgeoffrey.hessian.test;

public interface ITestService {
    
    public void emptyCall();
	
	public String callReturnsString();
	
	public String callReturnsYourString(String s);
	
	public String callThrowsException();
}
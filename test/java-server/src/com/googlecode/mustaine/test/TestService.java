package com.googlecode.mustaine.test;

public class TestService implements ITestService {

	public void emptyCall() {
		System.out.println("callWithoutReturn");
	}
	
	public String callReturnsString() {
		return "callReturnsString!";
	}
	
	public String callReturnsYourString(String s) {
		return s;
	}
	
	public String callThrowsException() {
	    throw new IllegalArgumentException("Your argument is illegal!");
	}
}

package com.royalgeoffrey.hessian.test;

public interface ITestService {
    
    public void emptyCall();
	
	public String callReturnsString();
	
	public String callReturnsUnicode();
	
	public String callReturnsYourString(String s);
	
	public String callThrowsException();
	
	public int callReturnsInt();
	
	public byte[] callReturnsBinary(byte[] payload);
	
	public boolean toggle(boolean input);
}
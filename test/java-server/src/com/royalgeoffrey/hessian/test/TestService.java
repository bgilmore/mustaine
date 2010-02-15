package com.royalgeoffrey.hessian.test;

import java.math.BigInteger;
import java.security.SecureRandom;

public class TestService implements ITestService {
	
	private SecureRandom random = new SecureRandom();

	public void emptyCall() {
		System.out.println("callWithoutReturn");
	}
	
	public String callReturnsString() {
		return "callReturnsString!";
	}
	
	public String callReturnsBigString() {
		return new BigInteger(130, random).toString(32);
	}
	
	public String callReturnsUnicode() {
		return "Unicodeª and ¹ (\ub9d0)";
	}
	
	public String callReturnsYourString(String s) {
		return s;
	}
	
	public String callThrowsException() {
	    throw new IllegalArgumentException("Your argument is illegal!");
	}
	
	public int callReturnsInt() {
		return 42;
	}
	
	public byte[] callReturnsBinary(byte[] payload) {
		return payload;
	}
	
	public boolean toggle(boolean input) {
		if (input) {
			return false;
		} else {
			return true;
		}
	}
}

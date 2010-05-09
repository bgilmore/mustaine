package com.googlecode.mustaine.testserver;

public interface ITestService
{  
  public void emptyCall();
  
  public String callReturnsString();
  
  public String callReturnsYourString(String s);
  
  public String callThrowsException();
}

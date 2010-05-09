package com.googlecode.mustaine.testserver;

import com.caucho.hessian.server.HessianServlet;

public class TestService extends HessianServlet implements ITestService
{  
  public void emptyCall() {
    ;
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

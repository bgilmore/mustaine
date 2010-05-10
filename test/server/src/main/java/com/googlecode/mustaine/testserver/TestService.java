package com.googlecode.mustaine.testserver;

import com.caucho.hessian.server.HessianServlet;
import java.util.Date;

public class TestService extends HessianServlet implements ITestService
{  
  public void emptyCall() {
    ;
  }
  
  public Boolean returnBool(Boolean b) {
    return b;
  }
  
  public Date returnDate(Date d) {
    return d;
  }
  
  public double returnDouble(double d) {
    return d;
  }
  
  public int returnInt(int i) {
    return i;
  }
  
  public long returnLong(long l) {
    return l;
  }
  
  public String returnString(String s) {
    return s;
  }
  
  public String callThrowsException() {
      throw new IllegalArgumentException("Your argument is illegal!");
  }
}

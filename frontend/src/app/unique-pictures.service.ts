import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';

import { throwError } from 'rxjs';
import { retry, catchError, tap, pluck } from 'rxjs/operators';
import { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UniquePicturesService {

  private SERVER_ADDRESS = "http://192.168.21.5:5000";
  private SERVER_URI = "/api/v1/pictures";
  // this may not be needed if flask-cors resolves the problem 
  //private httpOptions = {
    //headers: new HttpHeaders({
      //'Accept':  'application/json',
    //})
  //};
  public default_range: string = "page_starts_at=0000:00:00&range_start=0000:00:00&range_end=9999:99:99&page_size=5";
  public default_filter: string = "filter_string=";

  public first: string = "";  
  public last: string = "";  
  public after: string = "";  
  public before: string = "";
  constructor(private httpClient: HttpClient) { }

  handleError(error: HttpErrorResponse) {
    let errorMessage = 'Unknown error!';
    if (error.error instanceof ErrorEvent) {
      // Client-side errors
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side errors
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    window.alert(errorMessage);
    return throwError(errorMessage);
  }

  // In the tutorial, links first, last, prev, next as page numbers are in the Links header
  // but in our JSON::API approach, they are the links child of the body (and before/after ids not pages)
  parseLinkHeader(body) {
    if ((body !== undefined) && (body.links !== undefined)) {
      var links = body.links
      // only want the parameters
      this.first  = links["first"].split("?")[1];
      this.last   = links["last"].split("?")[1];
      this.before = links["before"].split("?")[1];
      this.after  = links["after"].split("?")[1]; 
    }
  }

  // FIXME need %4d:%2d:%2d
  make_date_str(d : Date) : string {
    return d.toISOString().split('T')[0]
    //return d.getFullYear() + ':' + d.getMonth() + ':' + d.getDate();
  }

  public make_range(start: Date, end: Date) : string {
    return("page_starts_at=" + this.make_date_str(start)
      + "&range_start=" + this.make_date_str(start)
      + "&range_end=" + this.make_date_str(end) 
      + "&page_size=5");
  }

  public sendGetRequestToUrl(url : string) {
    console.log("url: " + url)
    return this.httpClient.get(this.SERVER_ADDRESS + this.SERVER_URI, {
        params: new HttpParams({ fromString: url }), 
        observe: "response"})
      .pipe(retry(3), catchError(this.handleError), tap(res => {
        this.parseLinkHeader(res.body);
      }), pluck("body", "data"));
  }
  
  public sendPatchToUrl(id, tags) {
    // patch the tags field
    return this.httpClient.patch(this.SERVER_ADDRESS + this.SERVER_URI + "/" + id, 
      { 'tags': tags })
      .pipe(retry(3), catchError(this.handleError));
  }
}

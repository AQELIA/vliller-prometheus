import { Injectable } from '@nestjs/common';
import * as request from 'request';
import { ConfigService } from 'nestjs-config';

@Injectable()
export class AppService {
  constructor(private readonly config: ConfigService) {
    this.config = config;
  }

  getStationsData(): Promise<string> {
    return new Promise((resolve, reject) => {
      const url = `${this.config.get('vlille.apiBase')}&rows=-1&apikey=${this.config.get('vlille.apiKey')}`;

      request(url, { json: true }, (error, response, body) => {
        if (error) {
          return reject(error);
        }

        resolve(body);
      });
    });
  }
}

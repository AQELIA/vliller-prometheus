import { Get, Controller, Param } from '@nestjs/common';
import { AppService } from './app.service';

@Controller('miner')
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('vlille-stations')
  async getVlilleStationData(): Promise<string> {
    return this.appService.getStationsData();
  }
}

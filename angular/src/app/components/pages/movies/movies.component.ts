import { Component, OnInit } from '@angular/core';

import { SocketIoService } from '../../../services/socketio.service';
import { Movie } from '../../../models/movie.model';

@Component({
  selector: 'app-movies',
  templateUrl: './movies.component.html',
  styleUrls: ['./movies.component.scss']
})
export class MoviesComponent implements OnInit {

  public columns: string[] = ['title', 'tags', 'actions'];
  public movies: Movie[] = [];

  constructor(
    private socketIoService: SocketIoService,
  ) { }

  ngOnInit(): void {
    this.socketIoService.readMovies((movies: Movie[]) => {
      this.movies = movies;
    });
  }

  onDownload(movie: Movie): void {
    this.socketIoService.downloadMovie(movie);
  }

}

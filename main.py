import json
from typing import List, Optional

class Movie:
    """Класс, представляющий один фильм."""
    def __init__(self, title: str, genre: str, year: int, rating: float):
        if not title.strip():
            raise ValueError("Название не может быть пустым")
        if not genre.strip():
            raise ValueError("Жанр не может быть пустым")
        if not isinstance(year, int) or year < 1888:  # Год первого фильма
            raise ValueError("Год должен быть целым числом не менее 1888")
        if not isinstance(rating, (int, float)) or rating < 0 or rating > 10:
            raise ValueError("Рейтинг должен быть числом от 0 до 10")
        self.title = title.strip()
        self.genre = genre.strip()
        self.year = year
        self.rating = float(rating)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Movie':
        return cls(data['title'], data['genre'], data['year'], data['rating'])

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return (self.title == other.title and self.genre == other.genre 
                and self.year == other.year and self.rating == other.rating)

    def __repr__(self):
        return f"Movie('{self.title}', '{self.genre}', {self.year}, {self.rating})"


class MovieLibrary:
    """Управляет коллекцией фильмов: добавление, фильтрация, сохранение/загрузка."""
    def __init__(self):
        self.movies: List[Movie] = []

    def add_movie(self, movie: Movie) -> None:
        self.movies.append(movie)

    def remove_movie(self, index: int) -> None:
        if 0 <= index < len(self.movies):
            del self.movies[index]

    def filter_by_genre(self, genre: str) -> List[Movie]:
        if not genre.strip():
            return self.movies
        return [m for m in self.movies if m.genre.lower() == genre.strip().lower()]

    def filter_by_year(self, year: Optional[int]) -> List[Movie]:
        if year is None:
            return self.movies
        return [m for m in self.movies if m.year == year]

    def get_all_movies(self) -> List[Movie]:
        return self.movies

    def save_to_file(self, filepath: str) -> None:
        data = [m.to_dict() for m in self.movies]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_from_file(self, filepath: str) -> None:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.movies = [Movie.from_dict(item) for item in data]
        except FileNotFoundError:
            self.movies = []
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Ошибка чтения файла: {e}")

    def get_unique_genres(self) -> List[str]:
        return sorted(list({m.genre for m in self.movies}))
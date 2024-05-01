export interface Book {
  author: string;
  cover: string;
  rating: string;
  slug: string;
  synopsis: string;
  title: string;
  upvoted: boolean;
  upvotes: number;
}

export interface ApiBookResponse {
  books: Book[];
  meta: {
    count: number;
  };
}

export interface Comment {
  author: string;
  content: string;
}

export interface BookFrontEnd extends Book {
  ranking?: number;
  comments?: Comment[];
}

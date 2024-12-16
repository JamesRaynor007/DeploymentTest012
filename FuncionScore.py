
from fastapi import FastAPI, HTTPException
import pandas as pd
import os

# Definir la ruta del archivo CSV
file_path = os.path.join(os.path.dirname(__file__), 'FuncionScore.csv')

app = FastAPI()

df = pd.read_csv('FuncionScore.csv')
print(df.head())  # Verifica las primeras filas del DataFrame


@app.get("/score/")
async def get_movie(title: str):
    print(f"Buscando película: '{title}'")  # Muestra el título buscado
    movie = df[df['title'].str.lower() == title.lower()]
    print(f"Películas encontradas: {movie}")  # Muestra el DataFrame encontrado

    if movie.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie_data = movie.iloc[0]
    return {
        "title": movie_data['title'],
        "release_date": int(movie_data['release_year']),  # Convertir a int
        "vote_average": float(movie_data['vote_average'])  # Convertir a float
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/titles/")
async def get_titles():
    print("Llamando al endpoint /titles/")  # Para diagnóstico
    return df['title'].tolist()

# Instrucciones para ejecutar la aplicación:
# Ejecutar en la terminal: uvicorn main:app --reload

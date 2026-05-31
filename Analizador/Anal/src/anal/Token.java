/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package anal;

/**
 *
 * @author Home
 */
public class Token {
    public String id;
    public String contenido;
    public int fila;
    public int columna;

    public Token(String id, String contenido, int fila, int columna) {
        this.id = id;
        this.contenido = contenido;
        this.fila = fila;
        this.columna = columna;
    }

    @Override
    public String toString() {
        return String.format("\nToken{ID: %s | Contenido: %s | Fila: %d | Columna: %d}", id, contenido, fila, columna);
    }
}

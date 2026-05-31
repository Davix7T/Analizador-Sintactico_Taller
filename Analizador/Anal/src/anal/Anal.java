/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package anal;

import java.io.File;
import java.io.FileReader;
import java_cup.runtime.Symbol;

/**
 *
 * @author Home
 */
public class Anal {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
    try {
        String ruta = "src\\Anal\\fuente.txt";
        String archivo = new File(ruta).getAbsolutePath();
        
        // Inicializar lexer
        Lexer lex = new Lexer(new FileReader(archivo));
        
        // Ejecutar parser
        parser p = new parser(lex);
        p.parse(); // <-- AQUÍ SE EJECUTA EL ANÁLISIS SINTÁCTICO
        
        // Mostrar errores léxicos si existen
        if (lex.errlex.isEmpty()){
            System.out.println("Compilación correcta");
            System.out.println(lex.ts.toString());
        } else {
            System.err.println("Compilación con errores léxicos:");
            System.err.println(lex.errlex);
        }

    } catch (Exception e) {
        System.err.println("Error durante el análisis: " + e.getMessage());
    }
}

}

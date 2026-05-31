package anal;

import java.util.ArrayList;
import java_cup.runtime.*;

%%
%class Lexer
%line
%column
%cup



%{
    //para el manejo de errores
    public String errlex="";

    //para la tabla de simbolos (ts)
    public ArrayList<Token> ts = new ArrayList<Token>();

    // Clasifica los diferentes simbolos (Tokens) con CUP
    public Symbol symbol(int type){
        return new Symbol(type,yyline,yycolumn);
    }

    public Symbol symbol(int type, Object value) {
        return new Symbol(type, yyline, yycolumn, value);
    }
%}

/* ALFABETO */
LETRA = [a-zA-Z]
DIGITO = [0-9]
ESPACIO = [\n\t\r\f ]

NUMERO = "-"?{DIGITO}+ ("."{DIGITO})?
ID = {LETRA}({LETRA}|{DIGITO}|"_")*
CADENA = \"[^\"]*\"
OPARITMETICO = "+" | "-" | "*" | "/"
OPRELACIONAL = "<"|"<="|">="|"=="|"!="|">"
OPLOGICO = "|" | "&"

ASIGNACION = "="
PUNTOYCOMA = ";"
COMA = ","
DOSPUNTOS = ":"
PIZQUIERDO = "("
PDERECHO = ")"

PROGRAMA = "PROGRAM"|"Program"|"program" | "programa" | "Programa"
FINPROGRAMA = "ENDPROGRAM"|"EndProgram"|"endprogram"|"Endprogram"|"finprograma" | "FinPrograma"


TIPENTERO = "INT"|"Int"|"int"|"entero" | "Entero"
FLOAT = "FLOAT" | "float" | "Float" | "real" | "Real"
TIPSTRING = "STRING" | "string" | "String"

LEER = "READ"|"Read"|"read"|"leer" | "Leer"
ESCRIBIR = "WRITE"|"Write"|"write"|"escribir" | "Escribir"

SI = "IF"|"If"|"if"|"si" | "Si"
ENTONCES = "THEN"|"Then"|"then"|"entonces" | "Entonces"
SINO = "ELSE"|"Else"|"else"|"sino"
FINSI = "ENDIF"|"EndIf"|"Endif"|"endif"|"finsi" | "Finsi" | "Fin si"

MIENTRAS = "WHILE"|"While"|"while" | "Mientras"
HACER = "DO"|"Do"|"do" | "hacer" | "Hacer"
FINMIENTRAS = "ENDWHILE"|"EndWhile"|"Endwhile"|"endwhile" | "finMientras"

PARA = "FOR"|"For"|"for"|"para"
HASTA = "TO"|"To"|"to"|"hasta"
PASO = "STEP"|"Step"|"step"|"paso"
FINPARA = "ENDFOR"|"EndFor"|"Endfor"|"endfor"|"finpara" |"fin para"

SEGUN = "SWITCH"|"Switch"|"switch"|"segun" | "Segun"
CASO = "CASE" | "Case" | "case" | "caso"
DEOTROMODO = "DEFAULT"|"Default"|"default"|"deotromodo" | "De Otro Modo"
FINSEGUN = "ENDSWITCH"|"EndSwitch"|"Endswitch"|"endswitch"|"finsegun" "Fin Segun"

%%
{PROGRAMA} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.programa);}
{FINPROGRAMA} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.finprograma);}
{TIPENTERO} { ts.add(new Token("TYPE: Entero", yytext(), yyline, yycolumn)); return symbol(sym.tipo);}
{FLOAT} {ts.add(new Token("TYPE: Float", yytext(), yyline, yycolumn)); return symbol(sym.tipo);}
{TIPSTRING} { ts.add(new Token("TYPE: String", yytext(), yyline, yycolumn)); return symbol(sym.tipo);}
{LEER} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.leer);}
{ESCRIBIR} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.escribir);}
{SI} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.si);}
{ENTONCES} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.entonces);}
{SINO} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.sino);}
{FINSI} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.finsi);}
{MIENTRAS} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.mientras);}
{HACER} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.hacer);}
{FINMIENTRAS} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.finmientras);}
{PARA} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.para);}
{HASTA} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.hasta);}
{PASO} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.paso);}
{FINPARA} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.finpara);}
{SEGUN} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.segun);}
{CASO} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.caso);}
{DEOTROMODO} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.deotromodo);}
{FINSEGUN} { ts.add(new Token("Palabra Reservada", yytext(), yyline, yycolumn)); return symbol(sym.finsegun);}
{PIZQUIERDO} { ts.add(new Token("Parentesis Izquierdo", yytext(), yyline, yycolumn)); return symbol(sym.pi);}
{PDERECHO} { ts.add(new Token("Parentesis Derecho", yytext(), yyline, yycolumn)); return symbol(sym.pd);}
{DOSPUNTOS} { ts.add(new Token("Dos puntos", yytext(), yyline, yycolumn)); return symbol(sym.dospuntos);}
{PUNTOYCOMA} { ts.add(new Token("Punto y coma", yytext(), yyline, yycolumn)); return symbol(sym.puntocoma);}
{COMA} { ts.add(new Token("Coma", yytext(), yyline, yycolumn)); return symbol(sym.coma);}
{ASIGNACION} { ts.add(new Token("Asignacion", yytext(), yyline, yycolumn)); return symbol(sym.asig);}
{OPRELACIONAL} { ts.add(new Token("Operador Relacional", yytext(), yyline, yycolumn)); return symbol(sym.op_rel);}
{OPARITMETICO} { ts.add(new Token("Operador Aritmetico", yytext(), yyline, yycolumn)); return symbol(sym.op_ari);}
{OPLOGICO} { ts.add(new Token("Operador Logico", yytext(), yyline, yycolumn)); return symbol(sym.op_log);}
{ID} { ts.add(new Token("Identificador", yytext(), yyline, yycolumn)); return symbol(sym.id);}
{CADENA} { ts.add(new Token("Cadena (Comillas dobles)", yytext(), yyline, yycolumn)); return symbol(sym.cadena);}
{NUMERO} { ts.add(new Token("Numero", yytext(), yyline, yycolumn)); return symbol(sym.num);}
{ESPACIO} {}
. { errlex += "\nError Léxico en línea: " + (yyline+1) + ", columna: " + (yycolumn+1) + ", caracter no válido: " + yytext(); }

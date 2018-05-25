(*
    This is a Cool hello-world program.

    Implementer: Ruthenium Maxwell
        in 2018
*)

-- Standard Cool list
class List
{
    null () : Bool
    {
        true
    };

    car () : String
    {
        abort()
    };

    cdr () : List
    {
        abort()
    };

    cons (x : String) : List
    {
        (new Cons).init(x, self)
    };
};

class Cons inherits List
{
    head : String;
    tail : List;

    null () : Bool
    {
        false
    };

    car () : String
    {
        head
    };

    cdr () : List
    {
        tail
    };

    init (x : String, xs : List) : List
    {{
        head <- x;
        tail <- xs;
    }};
};

-- Program main class
class Main inherits IO
{
    -- Program entrance
    main () : SELF_TYPE
    {
        out_string("Hello, world"(* A nested comment block *))
    };
};

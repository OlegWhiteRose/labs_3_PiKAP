using System;
using System.Collections.Generic;


public abstract class GeometricShape
{
    public abstract double Area(); 
    public override string ToString()
    {
        return $"Shape area: {Area()}";
    }
}

public class Rectangle : GeometricShape, IPrint
{
    public double Width { get; set; }
    public double Height { get; set; }

    public Rectangle(double Width, double Height)
    {
        this.Width = Width;
        this.Height = Height;
    }

    public override double Area()
    {
        return Width * Height;
    }

    public override string ToString()
    {
        return $"Rectangle: Width = {Width}, Height = {Height}, Area = {Area()}";
    }

    public void Print()
    {
        Console.WriteLine(ToString());
    }
}

public class Square : Rectangle
{
    public double Side { get; set; }    

    public Square(double Side) : base(Side, Side) {}

    public override string ToString()
    {
        return $"Square: Side = {Side}, Area = {Area()}";
    }
}

public class Circle : GeometricShape, IPrint
{
    public double Radius { get; set; }

    public Circle(double Radius)
    {
        this.Radius = Radius;
    }

    public override double Area()
    {
        return Math.PI * Radius * Radius;
    }

    public override string ToString()
    {
        return $"Circle: Radius = {Radius}, Area = {Area()}";
    }

    public void Print()
    {
        Console.WriteLine(ToString());
    }
}

public interface IPrint
{
    void Print();
}

class Program
{
    static void Main(string[] args)
    {
        // Test 1:
        Rectangle rect = new Rectangle(5, 10);
        Square square = new Square(7);
        Circle circle = new Circle(3);

        rect.Print();
        square.Print();
        circle.Print();

        Console.WriteLine();
        
        // Test 2:
        List<IPrint> shapes = new List<IPrint>{new Rectangle(1.2, 2.2), new Square(3.2), new Circle(10)};
        foreach (var shape in shapes)
        {
            shape.Print();
        }
    }
}

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
    public double width { get; set; }
    public double height { get; set; }

    public Rectangle(double width, double height)
    {
        this.width = width;
        this.height = height;
    }

    public override double Area()
    {
        return width * height;
    }

    public override string ToString()
    {
        return $"Rectangle: Width = {width}, Height = {height}, Area = {Area()}";
    }

    public void Print()
    {
        Console.WriteLine(ToString());
    }
}

public class Square : Rectangle
{
    public Square(double side) : base(side, side){}

    public override string ToString()
    {
        return $"Square: Side = {width}, Area = {Area()}";
    }
}

public class Circle : GeometricShape, IPrint
{
    public double radius { get; set; }

    public Circle(double radius)
    {
        this.radius = radius;
    }

    public override double Area()
    {
        return Math.PI * radius * radius;
    }

    public override string ToString()
    {
        return $"Circle: Radius = {radius}, Area = {Area()}";
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

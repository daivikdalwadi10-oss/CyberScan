import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Landing from "../pages/Landing/index.jsx";

const renderLanding = () => {
  return render(
    <BrowserRouter>
      <Landing />
    </BrowserRouter>
  );
};

test("renders landing hero content", () => {
  renderLanding();
  expect(screen.getByText(/Enterprise Cyber Defense Platform/i)).toBeInTheDocument();
  expect(screen.getByText(/Modern vulnerability intelligence/i)).toBeInTheDocument();
});

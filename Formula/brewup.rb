class Brewup < Formula
  desc "One-command Homebrew update, upgrade, and cleanup"
  homepage "https://github.com/xcrong/brewup"
  license "MIT"

  livecheck do
    url :homepage
    strategy :github_latest
  end

  on_macos do
    on_arm do
      url "https://github.com/xcrong/brewup/releases/download/v0.3.0/brewup-aarch64-apple-darwin.tar.gz"
      sha256 "ae2d29dd096f89e099218343b122e71c86ef8155e30cb762390ff7a00a73b239"
    end
    on_intel do
      url "https://github.com/xcrong/brewup/releases/download/v0.3.0/brewup-x86_64-apple-darwin.tar.gz"
      sha256 "7d6e5c483699ad998eaa4426c1580620d1d5cf305d10ef50501a033155a4b199"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/xcrong/brewup/releases/download/v0.3.0/brewup-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "912c3bd1b2764787df4f33048c3ad01a9351148b18715e1d56b7c0bbff54a550"
    end
  end

  def install
    bin.install "brewup"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/brewup --version")
  end
end

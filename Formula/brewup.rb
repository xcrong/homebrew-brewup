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
      url "https://github.com/xcrong/brewup/releases/download/v0.2.1/brewup-aarch64-apple-darwin.tar.gz"
      sha256 "53d26a34769204964d9ede5042e81ffc538d37a0a26197950b0d12248480afa0"
    end
    on_intel do
      url "https://github.com/xcrong/brewup/releases/download/v0.2.1/brewup-x86_64-apple-darwin.tar.gz"
      sha256 "04daa41291b05dc52c94ec7fbb5d8a8a0c979dab8a621c1a89aba918ebe7a1b5"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/xcrong/brewup/releases/download/v0.2.1/brewup-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "d65fb771ca4614c3f613aa96c70b24c82f62a065b383cb19bbb26bcca12fe8d7"
    end
  end

  def install
    bin.install "brewup"
  end

  test do
    assert_match "brewup", shell_output("#{bin}/brewup --version")
  end
end
